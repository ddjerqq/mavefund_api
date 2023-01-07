const $close = document.querySelector(".close");
const $search = document.querySelector(".search-icon");
const $input = document.querySelector(".search-input");
const $wrapper = document.querySelector(".search-wrapper");

const searchToggle = () => {
	if ($wrapper.classList.contains("active")) {
        $input.value = '';
    }
    
    $wrapper.classList.toggle("active");
}

document.onkeydown = (e) => {
    if (e.key === "Enter") {
        let searchBar = document.getElementById("search-company");
        if (typeof searchBar !== "undefined") {
            let q = searchBar.value;
            window.location.replace(`/?q=${q}`);
        }
    }
}

function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.replace("/");
}

try {
    $search.addEventListener("click", searchToggle);
    $close.addEventListener("click", searchToggle);
    window.onload = function() {
        setTimeout(function(){
            $wrapper.classList.toggle("active")  //example function call.
        },250);
      }
} catch (e) {
    console.log(e);
}