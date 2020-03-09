// Copy link to clipboard

function addAlert(msg, cls) {
    let alert = document.createElement('div');
    let block = document.querySelector('.container');

    alert.innerHTML = msg;
    alert.classList.add('alert', cls, 'custom-alert');
    block.prepend(alert);
}

function removeAlert() {
    setTimeout(function() {
        $('.custom-alert').remove();
    }, 5000);
}

let btnsLink = document.querySelectorAll('.list__item_link');

btnsLink.forEach(item => {
  item.addEventListener('click', function(event) {
    event.preventDefault();

    let link = this.children[2];
    let range = document.createRange();
    range.selectNode(link);
    window.getSelection().addRange(range);

    try {
      document.execCommand('copy');
      addAlert('Ссылка скопирована <i class="fas fa-link fa-link_alert"></i>',
      'alert-success');
      removeAlert();
    } catch(err) {
      addAlert('Произошла ошибка \u{1F614}', 'alert-danger');
      removeAlert();
    }

    window.getSelection().removeAllRanges();
  });
})
