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