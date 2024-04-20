function openPayModal(first_name, last_name, currency_type, user_name) {
    let payModal = document.getElementById("payModal");
    document.getElementById("first_name").value = first_name;
    document.getElementById("last_name").value = last_name;
    document.getElementById("currency_type").value = currency_type;
    document.getElementById("user_name").value = user_name;
    payModal.style.display = "block";
}

function closePayModal() {
    let payModal = document.getElementById("payModal");
    payModal.style.display = "none";
}

function openRequestModal(request_first_name, request_last_name, request_currency_type, request_user_name) {
    let requestModal = document.getElementById("requestModal");
    document.getElementById("request_first_name").value = request_first_name;
    document.getElementById("request_last_name").value = request_last_name;
    document.getElementById("request_currency_type").value = request_currency_type;
    document.getElementById("request_user_name").value = request_user_name;

    requestModal.style.display = "flex";
}

function closeRequestModal() {
    let requestModal = document.getElementById("requestModal");
    requestModal.style.display = "none";
}

/*Add Money Modal*/
function openAddMoney() {
    let requestModal = document.getElementById("AddMoney");
    requestModal.style.display = "flex";
}

function closeAddMoney() {
    let requestModal = document.getElementById("AddMoney");
    requestModal.style.display = "none";
}

function openNotificationModal() {
    let requestModal = document.getElementById("NotificationModal");
    requestModal.style.display = "flex";
}

function closeNotificationModal() {
    let requestModal = document.getElementById("NotificationModal");
    requestModal.style.display = "none";
}

function openErrorModal() {
    let requestModal = document.getElementById("ErrorModal");
    requestModal.style.display = "flex";
}

function closeErrorModal() {
    let requestModal = document.getElementById("ErrorModal");
    requestModal.style.display = "none";
}
function openTransactionModal(transac_first_name, transac_last_name) {
    let TransactionModal = document.getElementById("TransactionModal");
    // document.getElementById("first_name").value = transac_first_name;
    // document.getElementById("last_name").value = transac_last_name;
    TransactionModal.style.display = "flex";
}

function closeTransactionModal() {
    let TransactionModal = document.getElementById("TransactionModal");
    TransactionModal.style.display = "none";
}

//Show Transactions
const toggleReceived = document.getElementById('toggle-received');
const toggleSent = document.getElementById('toggle-sent');
const receivedTransactions = document.getElementById('received-transactions');
const sentTransactions = document.getElementById('sent-transactions');
// Add click event listeners to the anchor tags
toggleReceived.addEventListener('click', function (event) {
    event.preventDefault();
    receivedTransactions.style.display = 'block';
    sentTransactions.style.display = 'none';
    // Update active class
    toggleReceived.classList.add('active');
    toggleSent.classList.remove('active');
});

toggleSent.addEventListener('click', function (event) {
    event.preventDefault();
    sentTransactions.style.display = 'block';
    receivedTransactions.style.display = 'none';
    // Update active class
    toggleSent.classList.add('active');
    toggleReceived.classList.remove('active');
});


