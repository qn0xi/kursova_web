document.addEventListener('DOMContentLoaded', function() {
    const dropdownMenu = document.querySelector('.dropdown-menu');
    const menuButton = document.querySelector('.menu-button');

    // Функція для закриття меню при кліку поза ним
    function closeMenu(event) {
        if (!dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('active');
            document.removeEventListener('click', closeMenu);
        }
    }

    // Обробник кліку по кнопці меню
    menuButton.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownMenu.classList.toggle('active');
        
        if (dropdownMenu.classList.contains('active')) {
            // Додаємо обробник для закриття меню при кліку поза ним
            setTimeout(() => {
                document.addEventListener('click', closeMenu);
            }, 0);
        } else {
            document.removeEventListener('click', closeMenu);
        }
    });

    // Закриваємо меню при кліку на пункт меню
    const menuItems = document.querySelectorAll('.dropdown-content a');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            dropdownMenu.classList.remove('active');
            document.removeEventListener('click', closeMenu);
        });
    });
}); 