from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

origins = ["*"]

app.add_middleware (
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
        )

async def number_api(number:int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://numbersapi.com/{number}/math")
        #return response.text
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error fetching fact from fact from Numbers API.")
        return response.text


@app.get("/api/classify-number")
async def root(number: str= None):
    if number is None:
        return {
                "number": number,
                "error": True
                }
    try:
        number = int(number)
    except ValueError:
        return {"number": number, "error": True}
    def is_prime(number):
        if number <= 1:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True


    def is_perfect(number):
        if number == 0:
            return False
        sum_1 = 0
        for i in range(1, number):
            if(number % i == 0):
                sum_1 = sum_1 + i
        if (sum_1 == number):
            return True
        return False

    def digit_sum(number):
        sum_1 = 0
        for digit in str(number):
            sum_1 = sum_1 +  int(digit)
        return sum_1
    
    def get_properties(number):

        properties = []

        def is_odd(number):
            if (number % 2) == 0:
                return "even"
            else:
                return "odd"

        def is_armstrong(number):

            number_str = str(number)

            n = len(number_str)
            armstrong_sum = 0

            for digit in number_str:
                armstrong_sum = armstrong_sum + int(digit) ** n

                if armstrong_sum == number:
                    return "armstrong"
                else:
                    None
        if is_armstrong(number):
            properties.append(is_armstrong(number))
        if is_odd(number):
            properties.append(is_odd(number))
        return properties

    number_fact = await number_api(number)

    return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": get_properties(number),
            "digit_sum": digit_sum(number),
            "fun_fact": number_fact
            }
