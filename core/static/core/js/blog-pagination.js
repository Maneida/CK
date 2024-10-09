// blog-pagination.js
document.addEventListener('DOMContentLoaded', function() {
    const content = document.querySelector('#blog-posts .container');
    const pagination = document.querySelector('#blog-pagination');

    if (content && pagination) {
        pagination.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                e.preventDefault();
                const url = e.target.href;
                fetchPage(url);
            }
        });
    }

    function fetchPage(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Update blog posts
                const newContent = doc.querySelector('#blog-posts .container');
                if (newContent) {
                    content.innerHTML = newContent.innerHTML;
                }

                // Update pagination
                const newPagination = doc.querySelector('#blog-pagination');
                if (newPagination) {
                    pagination.innerHTML = newPagination.innerHTML;
                }

                // Update URL without page reload
                history.pushState(null, '', url);

                // Scroll to top of blog posts section
                document.querySelector('#blog-posts').scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to normal page load on error
                window.location = url;
            });
    }
});