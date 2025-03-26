from lib.tools_model.prompts import search_recieves_prompt, extract_recieved_prompt
from lib.tools_model.schemas import RecieveBase, RecieveResult, ReportState, RecieveList
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send
from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv()

class ToolsModel:
    def __init__(self, model_name, model_type="ollama"):
        if model_type != "ollama":
            raise ValueError("Unsupported model type")
        
        self.llm = ChatOllama(model=model_name)
        self.tavily = TavilyClient()
        builder = StateGraph(ReportState)

        # Nodes
        builder.add_node("build_recieve", self.build_recieve)
        builder.add_node("single_recieve", self.single_recieve)
        builder.add_node("return_recieve", self.return_recieve)

        # Edges
        builder.add_edge(START, "build_recieve")
        builder.add_conditional_edges(
            "build_recieve", self.spaw_researchers, ["single_recieve"]
        )
        builder.add_edge("single_recieve", "return_recieve")
        builder.add_edge("return_recieve", END)
        
        self.graph = builder.compile()
        
    def find_recieves(self, ingredients : list[str]):
        return self.graph.invoke({"ingredients": ingredients})
    
    def build_recieve(self, state : ReportState):
        
        prompt = search_recieves_prompt.format(ingredients=",".join(state.ingredients))
        query_llm = self.llm.with_structured_output(RecieveList)
        result = query_llm.invoke(prompt)

        return {"recieves_names" : list(result.recieves)}

    def spaw_researchers(self, state : ReportState):
        return [
            Send("single_recieve", recieve) for recieve in state.recieves_names
        ]

    def single_recieve(self, recieve : str):

        results = self.tavily.search(
            f"Receita de {recieve}", 
            max_results=10, include_raw_content=False
        )

        for result in results["results"]:
            url = result["url"]
            try:
                url_extraction = self.tavily.extract(url)
                raw_content = url_extraction["results"][0]["raw_content"]

                query_llm = self.llm.with_structured_output(RecieveBase)
                result = query_llm.invoke(extract_recieved_prompt.format(content=raw_content))

                recieve_result =  RecieveResult(title=recieve.capitalize(), url= url, **result.model_dump())

                return {"recieves_results" : [recieve_result.model_dump()]}
            except:
                continue
    
    def return_recieve(self, state : ReportState):
        return {"recieves" : state.recieves_results}