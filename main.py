from fastapi import FastAPI
import google.generativeai as palm


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/prediction/")
async def prediction(rating:float,loan:float, down:float, appraised:float, 
                car:float, card:float, student:float, mortage:float, gross:float):
    ltv= (loan-down)/appraised
    dti= (car+card+student+mortage)/gross
    fedti= (mortage)/gross

    if((rating>=640.0) & (ltv<.8) & (dti<=0.43) & (fedti<=0.28)):
        message="Approved"
    else:
        message="Denied"

    if message=="Denied":
        prompt= f"""
            You are inquiring about a user's ability to purchase a home for Fannie Mae who answers questions based on potential inputs

            - Gross Monthly Income:{gross}
            - Credit Card Payment:{card}
            - Student Loan Payments:{student}
            - Appraised Value:{appraised}
            - Down Payment:{down}
            - Loan Amount:{loan}
            - Monthly Mortgage Payment{mortage}


            - Credit Score: {rating} 
            - LTV Ratio: {ltv*100}% (Calculated by Loan Amount - Down Payment / Appraised Value)
            - DTI Ratio: {dti*100}% (Calculated by total debt payments / gross monthly income)
            - FEDTI Ratio: {fedti*100}% (Calculated by total debt payments / gross monthly income)

            Based on the information provided, the user is not eligible, a user can purchase a home if Credit rating is 640 or above, LTV (loan-to-value) < 80% is preferred, between 80% and 95% could lead to a higher
            interest rate and require the purchase of mortgage insurance. DTI (Debt to income ratio) is the percentage of your gross monthly income that goes to
            paying your monthly debt payments and is used by lenders to determine your lending
            risk. Typically the highest DTI a lender will accept is 43% but in general lenders prefer
            ratios of not more than 36% with no more than 28% of that debt going towards servicing
            a mortgage. A “front-end debt to income” (FEDTI) ratio of less than or equal to 28%

            Give the user some advice on how to improve their chances of getting approved by evaluatin factors such as:
            - Pay off some current debt
            - Transfer debt to a ower interest rate loan /credit card
            - Look for a less expensive home
            - Increase your down payment amount
            - Continue renting while saving more for a down payment

            Make your response as friendly as possible and speak directly to the user. 

            """
        palm.configure(api_key='AIzaSyCJ3lbJtk6w5CQmklTuagFTKf4f_EOw1Fs')
        completion = palm.generate_text(
            model="models/text-bison-001", 
            prompt=prompt, 
            temperature=0.3,
            # The Maximum length of the response
            max_output_tokens=800,
        )

        result= completion.result  

    else:

        result= "Congratulations, you are eligible for a loan!! \n Here is a link to Fannie Mae's website with more information: https://yourhome.fanniemae.com/buy "

    return {"message": message, "result": result}
