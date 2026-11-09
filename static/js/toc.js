const links = new Map(
    [...document.querySelectorAll('.toc a[href^="#"]')].map(link => [decodeURIComponent(link.hash.slice(1)), link])
);
const headings = [...links.keys()].map(id => document.getElementById(id)).filter(Boolean);
const visible = new Set();
let active = null;

const setActive = id => {
    if (id === active) return;
    links.get(active)?.classList.remove('is-active');
    links.get(id)?.classList.add('is-active');
    active = id;
};

const observer = new IntersectionObserver(entries => {
    entries.forEach(({ target, isIntersecting }) => {
        isIntersecting ? visible.add(target) : visible.delete(target);
    });
    // Highlight the first visible heading; when none is, keep the last highlighted one.
    const first = headings.find(heading => visible.has(heading));
    if (first) setActive(first.id);
}, { rootMargin: '0px 0px -60% 0px' });

headings.forEach(heading => observer.observe(heading));
