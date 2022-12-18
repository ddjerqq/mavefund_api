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