const companies = [
    {key: 'AAPL', name: 'Apple'},
    {key: 'MSFT', name: 'Microsoft'},
    {key: 'AMZN', name: 'Amazon'},
    {key: 'GOOGL', name: 'Google'},
    {key: 'NFLX', name: 'Netflix'},
    {key: 'CNN', name: 'CNN'},
    {key: 'TSLA', name: 'Tesla'},
    {key: 'V', name: 'Visa'},
    {key: 'NVDA', name: 'Nvidia'},
    {key: 'WMT', name: 'Walmart'},
    {key: 'MA', name: 'MasterCard'},
    {key: 'KO', name: 'Coca-Cola'},
    {key: 'MCD', name: 'McDonald'},
    {key: 'NKE', name: 'Nike'},
    {key: 'CSCO', name: 'Cisco'},
    {key: 'DIS', name: 'Walt Disney'},
    {key: 'SBUX', name: 'Starbucks'},
    {key: 'PYPL', name: 'PayPal'},
];

$(document).ready(function() {
  if (localStorage.getItem('token')) {
    $('.nav-login-button').text('Logout')
  } else {
    $('.nav-login-button').text('Login')
  }
  $('.nav-login-button').click(function(e) {
    e.preventDefault();
    if (localStorage.getItem('token')) {
      localStorage.removeItem('token');
      location.reload();
    } else {
      location.href = '/signin.html'
    }
  })
    $('#modalSearchForm').submit((e) => {
        e.preventDefault();
        $('#docsearch-list').empty();
        
    $.ajax({
      url: `/api/v1/info/search?q=${$('#searchInput').val().toLowerCase()}`,
      success: function(res) {
        for (let key in res) {
          if (res[key]) {
            
    
            let company = `<li class="DocSearch-Hit" id="docsearch-item-0" role="option" aria-selected="true">
            <a class="no-underline" href="company.html?key=${key}">
              <div class="DocSearch-Hit-Container">
                <div>
                  <div class="DocSearch-Hit-icon">
                  </div>
                  <div class="DocSearch-Hit-content-wrapper"><span class="DocSearch-Hit-title"><strong>${key}</strong> ${res[key]}</span>
                  </div>
                </div>
                <div>
                 
                </div>
              </div>
            </a>
          </li>`;
            $('#docsearch-list').append(company);
          }
        }
      },
      error: function(err) {
        console.error(err)
      }
    })
    })
})