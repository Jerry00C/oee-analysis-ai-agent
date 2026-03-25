from db import query_supabase
from skills import get_daily_shift_data, get_oee_trend, get_top_scrap_day
from helper import print_result
from agent import agent


def test_skills():
    print(get_daily_shift_data('2021-03-16'))

    print(get_oee_trend('2021-03-09', '2021-03-16', '108 DC 800', 'DCM C3 108'))

    print(get_top_scrap_day('2021-03-09', '2021-03-16'))


def main():
    user_input = input("Ask your business analytics question: ")
    response = agent.invoke({"messages": [
        {"role": "user", "content": user_input}
        ]
    })
    for c in response["messages"]:
        print(c.content)

if __name__ == "__main__":
    main()

    test_skills()
    
