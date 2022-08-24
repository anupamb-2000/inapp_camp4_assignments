var delBtn = document.getElementById('deleteBtn');
delBtn.addEventListener("click", (e) => {
    var params = {
        'Name': document.getElementById("deleteName").innerHTML
    }
    fetch('http://127.0.0.1:5000/contacts/' + params['Name'].trim(), {
        method: 'delete'
    })
    .then(() => window.location.href="http://127.0.0.1:5000/contacts");
});