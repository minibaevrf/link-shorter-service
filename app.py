import redis
from flask import Flask, render_template, request, redirect
from link_shorter import LinkShorter
from applogger import AppLogger

logger = AppLogger.create_logger()
app = Flask(__name__)

redis_storage = redis.Redis(host='redis', port=6379)


@app.route('/')
def main():
    """Render home/main page.

    Returns:
      main.html template.
    """
    return render_template('main.html')


@app.route('/short_link', methods=['POST'])
def short_link():
    """Post request handler which shorts a given link.

    Returns:
        Short link of given link based on the current host, otherwise redirect to the error page (rendering
        error.html) with 500 code.
    """
    try:
        link_shorter = LinkShorter(redis_storage)

        source_link = request.form['link']
        result = link_shorter.save_link(source_link)

        return request.host_url + result
    except Exception as ex:
        logger.error("Incoming request to create short link %s failed with error - %s", short_link, ex)
        return render_template('error.html'), 500


@app.route('/<redirect_link>')
def redirect_short_link(redirect_link):
    """Redirect the given short link (alias) to the source link.

    Returns:
        Redirect to the source link, otherwise redirect to the error page (rendering error.html) with 500 code.
    """
    if redirect_link == 'favicon.ico':
        # ignore requesting favicon.ico
        return

    try:
        link_shorter = LinkShorter(redis_storage)
        result = link_shorter.get_source_link(redirect_link)

        if result is not None:
            return redirect(result, code=302)
        else:
            logger.warning("Couldn't found any saved links by short link %s", redirect_link)
            return render_template("link_not_found.html", link=request.host_url + redirect_link)
    except BaseException as ex:
        logger.error("When trying to process redirect by short link %s an critical error occurred - %s",
                     redirect_link, ex)
        return render_template('error.html'), 500


if __name__ == '__main__':
    """The main point of web service"""
    app.run()
