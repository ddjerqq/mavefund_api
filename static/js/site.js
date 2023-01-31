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
    $('.navbar-nav').append(`
    <li class="nav-item">
      <a class="nav-link" href="profile.html">Profile</a>
    </li>
    `);
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


$('.premium-btn').click(function(e) {
  e.preventDefault();
  checkout($(this).data('level'))
})

    const BASIC_PRICE_ID = "price_1MFS3GLGZqgNQZ5xIvlOvBHN";
const PREMIUM_PRICE_ID = "price_1MFS4MLGZqgNQZ5xHKDBEze7";
const SUPER_PRICE_ID = "price_1MFS5ILGZqgNQZ5xO4f2sl1Q";


async function createCheckoutSession(priceId) {
    const response = await fetch("/api/v1/stripe/create_checkout_session", {
        method: "POST",
        headers: {
            "content-type": "application/json",
            Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
            priceId: priceId,
        }),
    });

    return await response.json();
}


async function checkout(level) {
    let session;
    switch (level) {
        case 0:
            // basic
            session = await createCheckoutSession(BASIC_PRICE_ID);
            break;

        case 1:
            // premium
            session = await createCheckoutSession(PREMIUM_PRICE_ID);
            break;

        case 2:
            // super
            session = await createCheckoutSession(SUPER_PRICE_ID);
            break;
        default:
            alert("what are you trying to do exactly??? 🤨🤨🤨");
            break;
    }

    if (session.status === "success") {
        window.location.href = session.url;
    } else {
      console.log(session)
        if (session.detail === 'Unauthenticated') {
          location.href = '/signin.html'
        } else {
          const toast = new bootstrap.Toast(document.getElementById('liveToastBtn2'));
          toast.show();
        }
    }
}


})