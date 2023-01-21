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
                    <img src="https://logo.clearbit.com/${res[key]}.com" height="20px" width="20px"/>
                  </div>
                  <div class="DocSearch-Hit-content-wrapper"><span class="DocSearch-Hit-title"><strong>${key}</strong> ${res[key]}</span>
                  </div>
                </div>
                <div>
                  <div class="DocSearch-Hit-action"><button class="DocSearch-Hit-action-button"
                      title="Save this search" type="submit"><svg width="20" height="20" viewBox="0 0 20 20">
                        <path d="M10 14.2L5 17l1-5.6-4-4 5.5-.7 2.5-5 2.5 5 5.6.8-4 4 .9 5.5z"
                          stroke="currentColor" fill="none" fill-rule="evenodd" stroke-linejoin="round"></path>
                      </svg></button></div>
                  <div class="DocSearch-Hit-action"><button class="DocSearch-Hit-action-button"
                      title="Remove this search from history" type="submit"><svg width="20" height="20"
                        viewBox="0 0 20 20">
                        <path d="M10 10l5.09-5.09L10 10l5.09 5.09L10 10zm0 0L4.91 4.91 10 10l-5.09 5.09L10 10z"
                          stroke="currentColor" fill="none" fill-rule="evenodd" stroke-linecap="round"
                          stroke-linejoin="round"></path>
                      </svg></button></div>
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