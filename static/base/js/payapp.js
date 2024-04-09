function openPayModal(first_name, last_name, currency_type) {
    let payModal = document.getElementById("payModal");
    document.getElementById("first_name").value = first_name;
    document.getElementById("last_name").value = last_name;
    document.getElementById("currency_type").value = currency_type;
    payModal.style.display = "block";
}

function closePayModal() {
    let payModal = document.getElementById("payModal");
    payModal.style.display = "none";
}

function openRequestModal(request_first_name, request_last_name, request_currency_type ) {
    let requestModal = document.getElementById("requestModal");
    document.getElementById("request_first_name").value = request_first_name;
    document.getElementById("request_last_name").value = request_last_name;
    document.getElementById("request_currency_type").value = request_currency_type;
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
$('#toggle').click(function() {
    $('#transfers > .toggle-transactions').toggle('slow');
});

