# Removes unwanted chars
async def TrimData(data: str) -> str:
    try:
        characters_to_remove = ['(', ')', ',', "''", "'"]
        translation_table = str.maketrans('', '', ''.join(characters_to_remove))
        return data.translate(translation_table)  
    except Exception as e:
        print(e)
        return data