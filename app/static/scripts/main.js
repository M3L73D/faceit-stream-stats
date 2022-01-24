function copyToClipboard(text) {
    var $temp = $("<input>")
    $("body").append($temp)
    $temp.val(text).select()
    document.execCommand("copy")
    $temp.remove()
}

function composeSettings() {
    settings = {
        'nickname': $('.main-nickname').val(),
        'preset': 'RachelR',
        'select': $('.main-selector.select-date').val(),
        'select-input': $('.'+$('.main-selector.select-date').val() + '-input').val()
    }
    if(settings['select'] == 'from-date') {
        settings['select-input'] = Date.parse(settings['select-input']) / 1000
    } else {
        settings['select-input'] = parseInt(settings['select-input'])
    }
    return btoa(JSON.stringify(settings))
}

$(document).ready(function(){
    $('.main-selector.select-date').change(function(){
        $('.last-matches').addClass('hide')
        $('.from-date').addClass('hide')
        $('.in-last').addClass('hide')
        $('.'+$(this).val()).removeClass('hide')
    })
    $('.main-button.get-link').click(function(){
        composed = composeSettings()
        copyToClipboard(window.location.href + 'widget?token=' + composed)
        Toastify({
          text: "Ссылка скопирована в буфер обмена",
          duration: 3000,
          gravity: "bottom",
          position: "center",
          stopOnFocus: false,
          style: {
            "background": "linear-gradient(to right, #FF5CC4, #5CDAFF)",
            "font-family": "Caviar Dreams",
            "border-radius": "10px",
            "height:": "40px",
          }
        }).showToast();
    })
    $('.main-button.get-table').click(function(){
        composed = composeSettings()
        //window.open(window.location.href + 'table?token=' + composed, '_blank')
        window.location.href = window.location.href + 'table?token=' + composed
        Toastify({
          text: "Таблица генерируется...",
          duration: 3000,
          gravity: "bottom",
          position: "center",
          stopOnFocus: false,
          style: {
            "background": "linear-gradient(to right, #FF5CC4, #5CDAFF)",
            "font-family": "Caviar Dreams",
            "border-radius": "10px",
            "height:": "40px",
          }
        }).showToast();
    })
});