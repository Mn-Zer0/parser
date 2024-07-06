import aiohttp


async def get_vacancies(query: str, city: str, pages: int = 1):
    base_url = "https://api.hh.ru/vacancies"
    vacancies = []

    # Получение города по ID
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.hh.ru/suggests/areas?text={city}") as city_response:
            city_data = await city_response.json()
            if city_data['items']:
                city_id = city_data['items'][0]['id']
            else:
                raise ValueError(f"Город {city} не найден")

    params = {
        "text": query,
        "area": city_id,
        "search_field": "name",
        "per_page": 100
    }

    async with aiohttp.ClientSession() as session:
        for page in range(pages):
            params['page'] = page
            async with session.get(base_url, params=params) as response:
                result = await response.json()
                vacancies.extend(result['items'])

                if result['pages'] <= page:
                    break

    return vacancies