guard :shell do
    watch(/^(tests|gutter)(.*)\.py$/) do |match|
        puts `python setup.py nosetests`
    end
end

guard 'compass', project_path: 'gutter/web/media', configuration_file: 'gutter/web/media/config.rb' do
    watch(%r{.*scss})
end

guard 'coffeescript', input: 'gutter/web/media/coffee', output: 'gutter/web/media/js'

guard 'livereload' do
  watch(%r{media/.+\.(css|js)})
  watch(%r{templates/.+\.(html)})
  watch(%r{gutter/.+\.(py)})
end
