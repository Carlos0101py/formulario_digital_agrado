
function hiddenNotification(element) {
    element.style.display = "none"
};

document.addEventListener('DOMContentLoaded', () => {
    notification = document.querySelector('.notification_div')

    if (notification != null) {
        setTimeout(() => hiddenNotification(notification), 5000)
    }
});

document.addEventListener('DOMContentLoaded', () => {
    body = document.getElementById('anexoBody')
    inputFile = document.getElementById('anexo')
    parquivo = document.getElementById('NomeArquivo')

    body.addEventListener('click', () => {

        inputFile.click()

        inputFile.addEventListener('change', () => {

            const curFile = inputFile.files

            body.style.backgroundColor = '#14532D'

            for (file of curFile) {
                parquivo.textContent = file.name
            }
        })
    })
})



function divCheckOneStyle(element) {
    if (element.classList.contains('active')) {
        element.classList.remove('active')
        element.style.backgroundColor = ''

        description = element.getElementsByTagName('span')[0]
        description.style.color = ('')
    } else {
        element.classList.add('active')
        element.style.backgroundColor = ('#14532D')

        description = element.getElementsByTagName('span')[0]
        description.style.color = ('rgb(255, 255, 255, 1)')
    }
};

function toggleCheckOne(bodyDiv, clicked) {

    for (element of bodyDiv) {

        if (element.id) {
            if (element === clicked) {
                checkbox = element.querySelector('.checked')
                checkbox.checked = !checkbox.checked
            } else {
                checkbox = element.querySelector('.checked')
                element.classList.add('active')
                checkbox.checked = false;
            }

            divCheckOneStyle(element)
        }
    }
};

function toggleCheck(element) {

    checkbox = element.querySelector('.checked')
    checkbox.checked = !checkbox.checked
    divCheckOneStyle(element)
};

document.addEventListener('DOMContentLoaded', () => {

    bodyDiv = document.querySelectorAll('.bodyDiv')

    bodyDiv.forEach(element => {
        element.addEventListener('click', () => {

            element.id === "products" ? toggleCheckOne(bodyDiv, element) : toggleCheck(element);
        });
    });
}); 