🏠 MortgageMaster (Python)

A sleek, data-driven mortgage calculator built with Streamlit

MortgageMaster is your command center for decoding mortgage payments with clarity, precision, and zero nonsense. It transforms raw numbers into actionable insights — monthly payments, amortization schedules, interest breakdowns — all wrapped in an elegant and high-performance Streamlit dashboard.

🚀 Features
🎛️ Intuitive Input Panel

Select your currency (₹, $, €, £, ¥).

Enter home price, down payment, interest rate, and loan term.

Real-time calculation of down payment percentage.

Add-on cost modules:

Annual property tax

Annual insurance

Monthly HOA fees

📊 Dynamic Output Dashboard

Highlighted monthly payment figure with bold visual emphasis.

Donut chart breakdown (Principal & Interest, Property Tax, Insurance, HOA).

Summary KPI metrics:

Loan Amount

Total Interest

Total Cost of Mortgage

📉 Full Amortization Schedule

Month-by-month:

Principal paid

Interest paid

Cumulative interest

Remaining balance

Expandable table view.

Downloadable CSV export.

✨ Modern UI Enhancements

Custom metric cards

Wide layout configuration

Clean typography and consistent styling

Responsive two-column structure

🧮 Tech Stack
Technology	Purpose
Python	Core logic
Streamlit	Interactive web app
Pandas	Data wrangling + amortization schedule
NumPy	Computations
Altair	Donut visualization
📁 Project Structure
📂 MortgageMaster
│── app.py              # Main Streamlit app
│── README.md           # Project documentation
│── requirements.txt     # Dependencies (optional)

▶️ How to Run
1. Clone Repo
git clone <your-repo-url>
cd MortgageMaster

2. Install Dependencies
pip install -r requirements.txt

Required packages:
streamlit
pandas
numpy
altair

3. Launch App
streamlit run app.py


Your dashboard opens instantly in your browser. No server config. No fluff.

📸 Screenshots (Optional)

Add your own screenshots here for extra visual polish.

🧠 How It Works (Under the Hood)

Calculates principal, monthly interest rate, and number of payments.

Uses standard amortization formula for principal+interest.

Builds a full amortization schedule iteratively.

Renders UI + charts dynamically based on user input.

📤 Export Options

You can export the amortization schedule with a single click:

✔ CSV Download

✔ Formatted currency columns

✔ Scrollable clean table

✨ Author

🧑‍💻 Varsh Vishwakarma
AI • ML • DL • Data Science • Cloud • Full-Stack ML Developer
