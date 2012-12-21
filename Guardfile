guard :shell do
    watch(/^(tests|gutter)(.*)\.py$/) do |match|
        puts `python setup.py nosetests`
    end
end

guard 'compass', project_path: 'gutter/django/media', configuration_file: 'gutter/django/media/config.rb' do
    watch(%r{.*scss})
end

guard 'coffeescript', input: 'gutter/django/media/coffee', output: 'gutter/django/media/js'

guard 'livereload' do
  watch(%r{media/.+\.(css|js)})
  watch(%r{templates/.+\.(html)})
  watch(%r{gutter/.+\.(py)})
end
