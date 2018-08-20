echo '------------------------------------'
echo 'Running tests in local environment.'
echo '------------------------------------'

source venv/bin/activate
nosetests --rednose \
        --with-coverage \
        --no-byte-compile \
        --nologcapture \
        --nocapture \
        --cover-inclusive \
        --logging-level=CRITICAL \
        --cover-html \
        --with-id \
        --cover-html-dir=./coverage/ \
        -v