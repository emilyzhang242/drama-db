var gulp = require('gulp');

var clean           = require('gulp-clean');
var concat          = require('gulp-concat');
var imagemin        = require('gulp-imagemin');
var jshint          = require('gulp-jshint');
var minifycss       = require('gulp-minify-css');
var plumber         = require('gulp-plumber');
var rename          = require('gulp-rename');
var sass            = require('gulp-sass');
var stylish         = require('jshint-stylish');
var uglify          = require('gulp-uglify');
var declare         = require('gulp-declare');
var shell           = require('gulp-shell');

// compile SASS files
gulp.task('style', function(){
  return gulp.src('scripts/sass/*.scss')
    .pipe(plumber({
      errorHandler: function (err) {
        console.log(err);
        this.emit('end');
      }
    }))
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest(function( file ) { return path.join(path.dirname(file.path), 'static/css'); } ));
});

// minify and combine 3rd party scripts into one.
gulp.task('script-lib', function(){
  return gulp.src('scripts/javascript/libraries/*.js')
    .pipe(plumber({
      errorHandler: function (err) {
        console.log(err);
        this.emit('end');
      }
    }))
    .pipe(concat('lib.js'))
    .pipe(rename('lib.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(function( file ) { return path.join(path.dirname(file.path), 'static/js'); } ));
});

// minify custom scripts used in the website.
gulp.task('script-custom', function(){
  return gulp.src('scripts/javascript/custom/*.js')
    .pipe(plumber({
      errorHandler: function (err) {
        console.log(err);
        this.emit('end');
      }
    }))
    .pipe(jshint())
    .pipe(jshint.reporter(stylish))
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gulp.dest(function( file ) { return path.join(path.dirname(file.path), 'static/js'); } ));
});

gulp.task('script', ['script-lib', 'script-custom'], function(){});

gulp.task('watch', function(){
  gulp.watch('scripts/sass/**/*.scss', ['style']);
  gulp.watch('scripts/javascript/custom/*.js', ['script']);
  gulp.watch('scripts/javascript/libraries/*.js', ['script']);
});

gulp.task('default', ['style', 'script', 'watch'], function(){
  console.log('waiting...');
});
