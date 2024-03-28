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

