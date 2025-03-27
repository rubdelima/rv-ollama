from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from utils.ai.clarifai import get_ingredients_from_image
from utils.ai.tools_model.model import ToolsModel

app = FastAPI()

# Instanciar o modelo de IA (substitua os parâmetros conforme necessário)
tools_model = ToolsModel(model_name="gemini-2.0-flash", model_type="gemini")

@app.post("/generate-recipe/")
async def generate_recipe(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é uma imagem.")

    image_path = f"temp/{file.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extrai os ingredientes da imagem usando o Clarifai
    try:
        ingredients = get_ingredients_from_image(image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a imagem: {str(e)}")

    # Gera receitas usando os ingredientes
    try:
        result = tools_model.find_recieves(ingredients)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar receitas: {str(e)}")