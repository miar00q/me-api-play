// API base URL - change this when deploying
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://me-api-play.onrender.com';

// DOM elements
const skillSearchInput = document.getElementById('skill-search');
const keywordSearchInput = document.getElementById('keyword-search');
const searchBtn = document.getElementById('search-btn');
const profileContent = document.getElementById('profile-content');
const projectsContent = document.getElementById('projects-content');
const skillsContent = document.getElementById('skills-content');
const searchResultsSection = document.getElementById('search-results-section');
const searchResultsContent = document.getElementById('search-results-content');

// Utility functions
function showError(element, message) {
    element.className = 'error';
    element.textContent = message;
}

function showLoading(element, message = 'Loading...') {
    element.className = 'loading';
    element.textContent = message;
}

function hideSection(section) {
    section.classList.add('hidden');
}

function showSection(section) {
    section.classList.remove('hidden');
}

// API functions
async function fetchProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/profile`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching profile:', error);
        throw error;
    }
}

async function fetchProjectsBySkill(skill) {
    try {
        const response = await fetch(`${API_BASE_URL}/projects?skill=${encodeURIComponent(skill)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects by skill:', error);
        throw error;
    }
}

async function fetchTopSkills() {
    try {
        const response = await fetch(`${API_BASE_URL}/skills/top`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching top skills:', error);
        throw error;
    }
}

async function searchContent(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error searching content:', error);
        throw error;
    }
}

// Display functions
function displayProfile(profile) {
    profileContent.className = 'profile-info';

    const skillsHtml = profile.skills.map(skill =>
        `<span class="skill-tag">${skill.name}</span>`
    ).join('');

    const projectsHtml = profile.projects.map(project => `
        <div class="project-card">
            <h3>${project.title}</h3>
            <p>${project.description}</p>
            <div class="project-links">
                ${project.github_link ? `<a href="${project.github_link}" target="_blank">GitHub</a>` : ''}
                ${project.demo_link ? `<a href="${project.demo_link}" target="_blank">Demo</a>` : ''}
            </div>
        </div>
    `).join('');

    const workHtml = profile.work_experience.length > 0
        ? profile.work_experience.map(work => `
            <div class="profile-field">
                <label>${work.role} at ${work.company}</label>
                <span>${work.duration}</span>
            </div>
        `).join('')
        : '<p>No work experience listed</p>';

    profileContent.innerHTML = `
        <div class="profile-field">
            <label>Name</label>
            <span>${profile.name}</span>
        </div>
        <div class="profile-field">
            <label>Email</label>
            <span>${profile.email}</span>
        </div>
        <div class="profile-field">
            <label>Education</label>
            <span>${profile.education}</span>
        </div>
        <div class="profile-field">
            <label>Skills</label>
            <div class="skills-list">${skillsHtml}</div>
        </div>
        <div class="profile-field">
            <label>Projects</label>
            <div class="projects-grid">${projectsHtml}</div>
        </div>
        <div class="profile-field">
            <label>Work Experience</label>
            <div>${workHtml}</div>
        </div>
        ${profile.github_link ? `<div class="profile-field"><label>GitHub</label><span><a href="${profile.github_link}" target="_blank">${profile.github_link}</a></span></div>` : ''}
        ${profile.linkedin_link ? `<div class="profile-field"><label>LinkedIn</label><span><a href="${profile.linkedin_link}" target="_blank">${profile.linkedin_link}</a></span></div>` : ''}
        ${profile.portfolio_link ? `<div class="profile-field"><label>Portfolio</label><span><a href="${profile.portfolio_link}" target="_blank">${profile.portfolio_link}</a></span></div>` : ''}
    `;
}

function displayProjects(projects) {
    if (projects.length === 0) {
        projectsContent.innerHTML = '<p>No projects found for this skill.</p>';
        return;
    }

    const projectsHtml = projects.map(project => `
        <div class="project-card">
            <h3>${project.title}</h3>
            <p>${project.description}</p>
            <div class="project-links">
                ${project.github_link ? `<a href="${project.github_link}" target="_blank">GitHub</a>` : ''}
                ${project.demo_link ? `<a href="${project.demo_link}" target="_blank">Demo</a>` : ''}
            </div>
        </div>
    `).join('');

    projectsContent.innerHTML = `<div class="projects-grid">${projectsHtml}</div>`;
}

function displayTopSkills(skills) {
    if (skills.length === 0) {
        skillsContent.innerHTML = '<p>No skills found.</p>';
        return;
    }

    const skillsHtml = skills.map(skill => `
        <div class="skill-stat">
            <span class="skill-name">${skill.name}</span>
            <span class="skill-count">${skill.count}</span>
        </div>
    `).join('');

    skillsContent.innerHTML = `<div class="skills-stats">${skillsHtml}</div>`;
}

function displaySearchResults(results) {
    if (results.length === 0) {
        searchResultsContent.innerHTML = '<p>No results found.</p>';
        return;
    }

    const resultsHtml = results.map(result => `
        <div class="search-result-item">
            <h3>${result.title}</h3>
            <span class="type">${result.type}</span>
            <p>${result.description}</p>
            <div class="relevance">Relevance: ${(result.relevance_score * 100).toFixed(0)}%</div>
        </div>
    `).join('');

    searchResultsContent.innerHTML = `<div class="search-results">${resultsHtml}</div>`;
    showSection(searchResultsSection);
}

// Event handlers
async function handleSearch() {
    const skillQuery = skillSearchInput.value.trim();
    const keywordQuery = keywordSearchInput.value.trim();

    if (!skillQuery && !keywordQuery) {
        alert('Please enter a search term');
        return;
    }

    try {
        if (keywordQuery) {
            // Perform general search
            showLoading(searchResultsContent, 'Searching...');
            const results = await searchContent(keywordQuery);
            displaySearchResults(results);
        } else if (skillQuery) {
            // Search projects by skill
            showLoading(projectsContent, 'Searching projects...');
            const projects = await fetchProjectsBySkill(skillQuery);
            displayProjects(projects);
        }
    } catch (error) {
        if (keywordQuery) {
            showError(searchResultsContent, 'Error performing search. Please try again.');
        } else {
            showError(projectsContent, 'Error searching projects. Please try again.');
        }
    }
}

// Initialize the app
async function initApp() {
    try {
        // Load profile
        showLoading(profileContent);
        const profile = await fetchProfile();
        displayProfile(profile);

        // Load projects (show all projects initially)
        showLoading(projectsContent);
        const allProjects = await fetchProjectsBySkill(''); // Empty skill to get all
        displayProjects(profile.projects); // Use projects from profile instead

        // Load top skills
        showLoading(skillsContent);
        const topSkills = await fetchTopSkills();
        displayTopSkills(topSkills);

    } catch (error) {
        showError(profileContent, 'Error loading profile. Please check if the backend is running.');
        showError(projectsContent, 'Error loading projects.');
        showError(skillsContent, 'Error loading skills.');
    }
}

// Event listeners
searchBtn.addEventListener('click', handleSearch);
skillSearchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
});
keywordSearchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSearch();
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);
