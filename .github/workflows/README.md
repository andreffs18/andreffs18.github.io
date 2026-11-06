# Workflows

## `deploy.yml`

Builds the Hugo site and publishes it to GitHub Pages on every push to `master`.

### Why there is a "Setup Dart Sass" step

`layouts/partials/head.html` compiles `assets/css/main.scss` with Dart Sass (`transpiler: dartsass`). The older libsass transpiler is deprecated in Hugo and will be removed in a future release.

Hugo does not bundle Dart Sass. It runs a `sass` executable found on the `PATH` and talks to it over the embedded protocol, so the workflow installs it before the build:

```yaml
- name: Setup Dart Sass
  run: npm install -g sass-embedded@1.107.1
```
