module.exports = {
  less: {
    production: {
      options: {
        compress: true,
        sourceMap: false
      },
      files: {
        '<%= path.dest %>/css/main.css': '<%= path.src %>/less/*.less'
      }
    }
  },
  uglify: {
    scripts: {
     options: {
         sourceMap : {
           includeSources: true
         }
     },
      files: [{
        expand: true,
        cwd: '<%= path.src %>/js',
        src: '**/*.js',
        dest: '<%= path.dest %>/js'
      }]
    }
  },
  postcss: {
    production: {
      src: '<%= path.static %>/css/*.css',
      options: {
        map: false,
        processors: [
          require('autoprefixer')()
        ]
      }
    }
  }
};
