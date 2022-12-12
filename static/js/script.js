// todo make searchbar work
async function submit(e) {
    console.log(e);
    e.preventDefault();

    let ticker = document.getElementById("ticker").value;

    if (ticker === "") {
        alert("Please fill in all fields");
        return;
    }

    alert(`you are searching for ${ticker}`);
}
