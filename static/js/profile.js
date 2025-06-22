const input = document.getElementById('location');
const results = document.getElementById('location-results');

let timeout;

input.addEventListener('input', function () {
  clearTimeout(timeout);
  const query = this.value;

  if (query.length < 2) {
    results.innerHTML = '';
    return;
  }

  timeout = setTimeout(() => {
    fetch(`https://secure.geonames.org/searchJSON?name=${encodeURIComponent(query)}&featureClass=P&maxRows=10&username=djpotts2891`)
      .then(res => res.json())
      .then(data => {
        results.innerHTML = '';
        if (data.geonames && data.geonames.length > 0) {
          data.geonames.forEach(place => {
            const li = document.createElement('li');
            li.className = 'list-group-item list-group-item-action';
            li.textContent = `${place.name}, ${place.countryName}`;
            li.addEventListener('click', () => {
              input.value = `${place.name}, ${place.countryName}`;
              results.innerHTML = '';
            });
            results.appendChild(li);
          });
        } else {
          const li = document.createElement('li');
          li.className = 'list-group-item disabled';
          li.textContent = 'No results found';
          results.appendChild(li);
        }
      })
      .catch(() => {
        results.innerHTML = '<li class="list-group-item disabled">Error fetching results</li>';
      });
  }, 300); // Debounce delay
});