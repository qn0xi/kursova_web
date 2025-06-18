document.addEventListener('DOMContentLoaded', function() {
    const dropdownMenu = document.querySelector('.custom-dropdown-menu');
    const menuButton = document.querySelector('.custom-menu-button');

    function closeMenu(event) {
        if (!dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('active');
            document.removeEventListener('click', closeMenu);
        }
    }

    menuButton.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownMenu.classList.toggle('active');
        
        if (dropdownMenu.classList.contains('active')) {
            setTimeout(() => {
                document.addEventListener('click', closeMenu);
            }, 0);
        } else {
            document.removeEventListener('click', closeMenu);
        }
    });

    const menuItems = document.querySelectorAll('.custom-dropdown-content a');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            dropdownMenu.classList.remove('active');
            document.removeEventListener('click', closeMenu);
        });
    });
});

// JavaScript for seat_selection.html
document.addEventListener('DOMContentLoaded', function() {
    const seats = document.querySelectorAll('.seat.seat-available, .seat.seat-vip');
    const selectedSeatsList = document.getElementById('selected-seats-list');
    const ticketCountSpan = document.getElementById('ticket-count');
    const totalPriceSpan = document.getElementById('total-price');
    const buyTicketsBtn = document.getElementById('buy-tickets-btn');
    const priceBreakdownDiv = document.getElementById('price-breakdown');

    if (buyTicketsBtn && selectedSeatsList && ticketCountSpan && totalPriceSpan && priceBreakdownDiv) {
        let selectedSeats = [];

        seats.forEach(seat => {
            seat.addEventListener('click', function() {
                if (this.classList.contains('seat-sold')) {
                    return;
                }

                if (this.classList.contains('seat-selected')) {
                    this.classList.remove('seat-selected');
                    this.classList.add(this.dataset.originalClass);
                    selectedSeats = selectedSeats.filter(s => s !== this);
                } else {
                    this.dataset.originalClass = this.classList.contains('seat-available') ? 'seat-available' : 'seat-vip';
                    this.classList.add('seat-selected');
                    this.classList.remove('seat-available');
                    this.classList.remove('seat-vip');
                    selectedSeats.push(this);
                }
                updateSummary();
            });
        });

        buyTicketsBtn.addEventListener('click', function() {
            if (selectedSeats.length === 0) return;
            const seatsPayload = selectedSeats.map(seat => ({
                row: seat.dataset.row,
                seat: seat.dataset.seat,
                type: seat.dataset.originalClass === 'seat-vip' ? 'VIP місце' : 'Звичайне місце',
                price: seat.dataset.price
            }));
            fetch(window.location.pathname.replace('/select_seats/', '/purchase/'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ seats: seatsPayload })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Дякуємо за покупку! Лист надіслано на вашу пошту.');
                    window.location.reload();
                } else {
                    alert('Помилка: ' + (data.error || 'Щось пішло не так.'));
                }
            })
            .catch(() => alert('Помилка при відправці запиту.'));
        });

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function updateSummary() {
            let count = selectedSeats.length;
            let total = 0;
            let seatsText = [];
            let vipTicketCount = 0;
            let regularTicketCount = 0;
            let vipTotalPrice = 0;
            let regularTotalPrice = 0;

            selectedSeats.forEach(seat => {
                const price = parseInt(seat.dataset.price);
                const row = seat.dataset.row;
                const seatNum = seat.dataset.seat;
                const seatType = seat.dataset.originalClass === 'seat-vip' ? 'VIP Місце' : 'Звичайне Місце';
                const seatDescription = `${seatType} (Ряд ${row}, Місце ${seatNum})`;

                total += price;
                seatsText.push(seatDescription);

                if (seat.dataset.originalClass === 'seat-vip') {
                    vipTicketCount++;
                    vipTotalPrice += price;
                } else {
                    regularTicketCount++;
                    regularTotalPrice += price;
                }
            });

            selectedSeatsList.textContent = seatsText.length > 0 ? seatsText.join(', ') : 'Не вибрано';
            ticketCountSpan.textContent = count;

            let breakdownHtml = '';
            if (regularTicketCount > 0) {
                breakdownHtml += `<p>Звичайні квитки: ${regularTicketCount} x ${regularTotalPrice / regularTicketCount} UAH = <span>${regularTotalPrice} UAH</span></p>`;
            }
            if (vipTicketCount > 0) {
                breakdownHtml += `<p>VIP квитки: ${vipTicketCount} x ${vipTotalPrice / vipTicketCount} UAH = <span>${vipTotalPrice} UAH</span></p>`;
            }
            priceBreakdownDiv.innerHTML = breakdownHtml;

            totalPriceSpan.textContent = total;
            buyTicketsBtn.disabled = count === 0;
        }
    }
});

// JavaScript for schedule.html
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('schedule-date');
    const schedulesContainer = document.getElementById('schedules-container');

    if (dateInput && schedulesContainer) {
        const today = new Date();
        const todayString = today.toISOString().split('T')[0];
        dateInput.setAttribute('min', todayString);

        dateInput.addEventListener('change', function() {
            const selectedDate = this.value;
            if (selectedDate) {
                fetch(`/schedule/by-date/?date=${selectedDate}`)
                    .then(response => response.json())
                    .then(data => {
                        schedulesContainer.innerHTML = '';
                        if (data.schedules && data.schedules.length > 0) {
                            const schedulesByMovie = data.schedules.reduce((acc, schedule) => {
                                if (!acc[schedule.movie_title]) {
                                    acc[schedule.movie_title] = {
                                        poster_url: schedule.poster_url,
                                        age_rating: schedule.age_rating,
                                        format: schedule.format,
                                        percentage_category: schedule.percentage_category,
                                        sessions: []
                                    };
                                }
                                acc[schedule.movie_title].sessions.push({
                                    time: schedule.time,
                                    hall: schedule.hall,
                                    price: schedule.price,
                                    id: schedule.id
                                });
                                return acc;
                            }, {});

                            for (const movieTitle in schedulesByMovie) {
                                const movieData = schedulesByMovie[movieTitle];
                                const movieCard = document.createElement('div');
                                movieCard.classList.add('movie-card_schedule');

                                let sessionsHtml = '';
                                movieData.sessions.forEach(session => {
                                    sessionsHtml += `
                                        <a href="/schedule/${session.id}/select_seats/" class="session-button_schedule">
                                            <div class="session-time_schedule">${session.time}</div>
                                            <div class="session-hall_schedule">Зал №${session.hall}</div>
                                        </a>
                                    `;
                                });

                                movieCard.innerHTML = `
                                    <div class="movie-poster_schedule">
                                        <img src="${movieData.poster_url}" alt="Movie Poster">
                                    </div>
                                    <div class="movie-details_schedule">
                                        <h3 class="movie-title_schedule">${movieTitle}</h3>
                                        <div class="movie-meta_schedule">
                                            ${movieData.age_rating ? `<span class="meta-tag_schedule age-rating_schedule">${movieData.age_rating}</span>` : ''}
                                            ${movieData.format ? `<span class="meta-tag_schedule format_schedule">${movieData.format}</span>` : ''}
                                            ${movieData.percentage_category ? `<span class="meta-tag_schedule percentage-category_schedule">${movieData.percentage_category}%</span>` : ''}
                                        </div>
                                        <p class="sessions-title_schedule">Сеанси:</p>
                                        <div class="sessions_schedule">
                                            ${sessionsHtml}
                                        </div>
                                    </div>
                                `;

                                schedulesContainer.appendChild(movieCard);
                            }

                        } else {
                            schedulesContainer.innerHTML = '<p>На цю дату розкладів немає.</p>';
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching schedules:', error);
                        schedulesContainer.innerHTML = '<p>Помилка завантаження розкладу.</p>';
                    });
            }
        });

        dateInput.value = todayString;
        dateInput.dispatchEvent(new Event('change'));
    }
});

// JavaScript for purchase_history.html
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.stars .star');
    const submitButtons = document.querySelectorAll('.submit-rating-btn');

    function initializeStars() {
        document.querySelectorAll('.stars').forEach(starContainer => {
            const movieId = starContainer.dataset.movieId;
            const existingRating = starContainer.dataset.existingRating;
            if (existingRating && existingRating !== 'None') {
                starContainer.querySelectorAll('.star').forEach(star => {
                    if (parseInt(star.dataset.value) <= parseInt(existingRating)) {
                        star.classList.add('active');
                    }
                });
                const submitButton = starContainer.closest('.rating-section').querySelector('.submit-rating-btn');
                if (submitButton) {
                    submitButton.dataset.rating = existingRating;
                    submitButton.disabled = false;
                }
            }
        });
    }

    initializeStars();

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const movieId = this.closest('.stars').dataset.movieId;
            const rating = this.dataset.value;
            document.querySelectorAll(`.stars[data-movie-id="${movieId}"] .star`).forEach(s => s.classList.remove('active'));

            document.querySelectorAll(`.stars[data-movie-id="${movieId}"] .star`).forEach(s => {
                if (s.dataset.value <= rating) {
                    s.classList.add('active');
                }
            });
            
            document.querySelectorAll(`.submit-rating-btn[data-movie-id="${movieId}"]`).forEach(submitBtn => {
                submitBtn.disabled = false;
                submitBtn.dataset.rating = rating;
            });
        });

        star.addEventListener('mouseover', function() {
            const movieId = this.closest('.stars').dataset.movieId;
            const hoverRating = this.dataset.value;
            document.querySelectorAll(`.stars[data-movie-id="${movieId}"] .star`).forEach(s => {
                if (s.dataset.value <= hoverRating) {
                    s.classList.add('hover');
                } else {
                    s.classList.remove('hover');
                }
            });
        });

        star.addEventListener('mouseout', function() {
            const movieId = this.closest('.stars').dataset.movieId;
            document.querySelectorAll(`.stars[data-movie-id="${movieId}"] .star`).forEach(s => s.classList.remove('hover'));
        });
    });

    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const movieId = this.dataset.movieId;
            const rating = this.dataset.rating;
            console.log(`[Submit Click] Movie ID: ${movieId}, Button Data-rating (before check): ${rating}`);

            if (!rating) {
                alert('Будь ласка, оберіть оцінку.');
                return;
            }

            fetch('/submit_rating/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ movie_id: movieId, rating: rating })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Ваша оцінка успішно надіслана!');
                } else {
                    alert('Помилка: ' + (data.error || 'Не вдалося надіслати оцінку.'));
                }
            })
            .catch(() => alert('Помилка при відправці запиту.'));
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// JavaScript for movie_gallery.html
document.addEventListener('DOMContentLoaded', function() {
    var movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach(function(card) {
        card.addEventListener('click', function() {
            var movieId = this.dataset.movieId;
            fetch(`/movies/details/${movieId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('movieDetailModalLabel').textContent = data.title;
                    document.getElementById('modalMoviePoster').src = data.poster;
                    document.getElementById('modalMovieDescription').textContent = data.movie;
                    document.getElementById('modalMovieAgeRating').textContent = data.age_rating;
                    document.getElementById('modalMovieFormat').textContent = data.format;
                    document.getElementById('modalMovieDuration').textContent = data.duration_minutes;
                    document.getElementById('modalMovieGenres').textContent = data.genres;
                    document.getElementById('modalMovieActors').textContent = data.actors;
                    document.getElementById('modalMoviePublisher').textContent = data.publisher;
                    document.getElementById('modalMovieStatus').textContent = data.status_display;
                    document.getElementById('modalMovieAverageRating').textContent = data.average_rating;

                    var trailerDiv = document.getElementById('modalMovieTrailer');
                    trailerDiv.innerHTML = '';
                    if (data.trailer_url) {
                        console.log('Trailer URL found:', data.trailer_url);
                        var youtubeId = getYouTubeId(data.trailer_url);
                        if (youtubeId) {
                            console.log('YouTube ID extracted:', youtubeId);
                            var iframe = document.createElement('iframe');
                            iframe.src = `https://www.youtube.com/embed/${youtubeId}`;
                            iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
                            iframe.allowFullscreen = true;
                            iframe.classList.add('modal-trailer-iframe');
                            trailerDiv.appendChild(iframe);
                        }
                    }

                    var buyTicketButton = document.getElementById('buyTicketButton');
                    if (data.sessions && data.sessions.length > 0) {
                        var firstSessionId = data.sessions[0].id;
                        buyTicketButton.href = `/schedule/`;
                        buyTicketButton.style.display = 'inline-block';
                    } else {
                        buyTicketButton.style.display = 'none';
                    }

                    var movieDetailModal = new bootstrap.Modal(document.getElementById('movieDetailModal'));
                    movieDetailModal.show();
                    console.log('Modal shown.');
                })
                .catch(error => console.error('Error fetching movie details:', error));
        });
    });

    function getYouTubeId(url) {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
        var match = url.match(regExp);
        return (match && match[2].length === 11) ? match[2] : null;
    }
}); 