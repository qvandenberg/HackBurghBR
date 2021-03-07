# HackBurghBR
BlackRock challenge Hack the Burgh 2021

## Challenge motivation
Our goal here was to make a tool that helps small, beginning investors get started with investing in stocks. 
The stock market has far higher returns than most savings accounts, but there is a knowledge and trust barrier
to entry. We want to overcome this by selecting a reliable ETF index, and propose an investment portfolio that
consists of stocks + cash savings.

Clients provide some basic details about their financial situation and length of time they want to invest for,
and we simulate the optimum mix of cash savings and stock market investment. As the expiry time approaches, we 
gradually reduce the amount of invested money to provide a low-risk exit.

Simulations are done with Monte Carlo simulations based on historical data of the QQQ ETF index (Nasdaq 100). The data is collected
through an API and this code will remain valid in the future as well (we don't use any hard-coded data). We want to give a best and worse case scenario, and
also compare the situation with and without investments to demonstrate the added value of investment.

## Back-end
The back-end is written in a Python Flask app. The app collects data from Alpha Vantage through their API. 
The `src/server/app.py` also contains the Monte Carlo simulations used to calculate the upper and lower bounds of the expected returns.

## Front-end
The front-end is an Android app written in Java. This is where the user enters the data, and this part of the code calls the API in the back-end.
