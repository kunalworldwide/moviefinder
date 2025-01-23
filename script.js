// API key is stored in a separate config file for security
const TMDB_API_KEY = ''; // Use the API key provided by user
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

async function searchTMDB(query) {
  try {
    const response = await fetch(
      `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}`
    );
    
    if (!response.ok) {
      throw new Error(`TMDB API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Error searching TMDB:', error);
    return [];
  }
}

// DOM Elements
const searchInput = document.getElementById('search-input');
const resultsContainer = document.getElementById('results');

// Debounce function
function debounce(func, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

// Search function
async function searchMovies(query) {
  console.log('Searching TMDB for:', query);
  resultsContainer.innerHTML = '<div class="loading">Searching TMDB...</div>';
  
  try {
    const movies = await searchTMDB(query);
    console.log('Found', movies.length, 'matches');
    displayResults(movies);
  } catch (error) {
    console.error('Search error:', error);
    resultsContainer.innerHTML = '<div class="error">Error searching movies. Please try again.</div>';
  }
}

// Display results
function displayResults(movies) {
  resultsContainer.innerHTML = '';
  
  if (movies.length === 0) {
    resultsContainer.innerHTML = '<div class="no-results">No movies found</div>';
    return;
  }
  
  movies.forEach(movie => {
    const card = document.createElement('div');
    card.className = 'movie-card';
    
    const posterUrl = movie.poster_path 
      ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
      : 'https://via.placeholder.com/500x750?text=No+Poster';
      
    const releaseYear = movie.release_date 
      ? new Date(movie.release_date).getFullYear()
      : 'Unknown year';
      
    card.innerHTML = `
      <img class="movie-poster" src="${posterUrl}" alt="${movie.title}">
      <div class="movie-info">
        <h3 class="movie-title">${movie.title} (${releaseYear})</h3>
        <div class="movie-details">
          <span>${movie.vote_average}/10</span> | 
          <span>${movie.popularity} popularity</span>
        </div>
        <p>${movie.overview || 'No description available'}</p>
      </div>
    `;
    
    resultsContainer.appendChild(card);
  });
}

// Event listeners
searchInput.addEventListener('input', debounce((e) => {
  const query = e.target.value.trim();
  if (query.length > 2) {
    searchMovies(query);
  } else {
    resultsContainer.innerHTML = '';
  }
}, 300));
