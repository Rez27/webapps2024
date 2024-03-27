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

function openRequestModal() {
    let requestModal = document.getElementById("requestModal");
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

