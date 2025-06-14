import streamlit as st
import requests

st.title("Bank Application")


if 'action' not in st.session_state:
    st.session_state.action = None


st.sidebar.header("Operations")
operations = {
    "Create Account": "create",
    "Credit Amount": "credit",
    "Debit Amount": "debit",
    "Transfer Funds": "transfer",
    "User Details": "details",
    "Clear": None
}

for label, value in operations.items():
    if st.sidebar.button(label):
        st.session_state.action = value


if st.session_state.action == "create":
    st.subheader("Create New Bank Account")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    acc_no = st.text_input("Account Number")
    ifsc = st.text_input("IFSC Code")
    branch_name = st.text_input("Branch Name")
    balance = st.text_input("Initial Balance (default 0.0)", value="0.0")

    if st.button("Create Account",key="create_button"):
        if not all([first_name, last_name, acc_no, ifsc, branch_name, balance]):
            st.warning("Please fill all fields.")
        else:
            try:
                data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "acc_no": acc_no,
                    "ifsc": ifsc,
                    "branch_name": branch_name,
                    "balance": balance
                }
                res = requests.post("http://127.0.0.1:8000/user/create", params=data)
                if res.status_code == 200:
                    st.success("Account created successfully.")
                else:
                    st.error(f"Failed to create account: {res.json()}")
            except Exception as e:
                st.error(f"Error: {e}")


elif st.session_state.action == "credit":
    st.subheader("Credit Amount")
    acc_no = st.text_input("acc_no")
    amt = st.text_input("amt")

    if st.button("Credit",key="credit_button"):
        if not acc_no or not amt:
            st.warning("Please enter account number and amount.")
        else:
            try:
                res = requests.post("http://127.0.0.1:8000/user/credit", params={"acc_no": acc_no, "amt": float(amt)})
                if res.status_code == 200:
                    st.success(f"Amount credited. New balance: {res.json().get('current balance')}")
                else:
                    st.error(f"Failed to credit: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")


elif st.session_state.action == "debit":
    st.subheader("Debit Amount")
    acc_no = st.text_input("acc_no")
    amt = st.text_input("amt")

    if st.button("Debit",key="debit_button"):
        if not acc_no or not amt:
            st.warning("Please enter account number and amount.")
        else:
            try:
                res = requests.post("http://127.0.0.1:8000/user/debit", params={"acc_no": acc_no, "amt": float(amt)})
                if res.status_code == 200:
                    response = res.json()
                    if isinstance(response, dict) and "message" in response:
                        st.error(response["message"])
                    else:
                        st.success(f"Amount debited. New balance: {response}")
                else:
                    st.error(f"Failed to debit: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")


elif st.session_state.action == "transfer":
    st.subheader("Transfer Funds")
    f_acc = st.text_input("From Account")
    to_acc = st.text_input("To Account")
    amt = st.text_input("amt")

    if st.button("Transfer",key="transfer_button"):
        if not all([f_acc, to_acc, amt]):
            st.warning("Please fill all fields.")
        else:
            try:
                res = requests.get("http://127.0.0.1:8000/user/transfer", params={
                    "f_acc": f_acc,
                    "to_acc": to_acc,
                    "amt": float(amt)
                })
                if res.status_code == 200:
                    st.success(res.json().get("message"))
                else:
                    st.error(f"Transfer failed: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")


elif st.session_state.action == "details":
    st.subheader("User Details")
    acc_no = st.text_input("acc_no")

    if st.button("Show Details",key="details_button"):
        if not acc_no:
            st.warning("Enter an account number.")
        else:
            try:
                res = requests.get("http://127.0.0.1:8000/user/details", params={"acc_no": acc_no})
                if res.status_code == 200:
                    rows = res.json()
                    if rows:
                        for row in rows:
                            st.write(
                                f"Account No: {row[1]}, IFSC: {row[2]}, Branch: {row[3]}, Name: {row[4]} {row[5]}, Balance: ₹{row[6]}"
                            )
                    else:
                        st.info("No account found.")
                else:
                    st.error(f"Failed to fetch details: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")


else:
    st.write("Select an operation from the sidebar to begin.")



