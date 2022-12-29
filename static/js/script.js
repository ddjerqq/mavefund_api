const $close = document.querySelector(".close")
const $search = document.querySelector(".search-icon")
const $input = document.querySelector(".search-input")
const $wrapper = document.querySelector(".search-wrapper")

const searchToggle = () => {
	if ($wrapper.classList.contains("active")) $input.value = ''
    
    $wrapper.classList.toggle("active")
}

$search.addEventListener("click", searchToggle)
$close.addEventListener("click", searchToggle)

window.onload = function() {
    setTimeout(function(){
        $wrapper.classList.toggle("active")  //example function call.    
    },250);
};

function get_cookie(name){
    return document.cookie.split(';').some(c => {
        return c.trim().startsWith(name + '=');
    });
}

function logout() {
  if( get_cookie( "token" ) ) {
    document.cookie = "token=;expires=Thu, 01 Jan 1970 00:00:01 GMT";
    location.reload();
  }
}