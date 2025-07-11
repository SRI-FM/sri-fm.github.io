# Website for the Formal Methods Program @ SRI

## Editing

The website is built with the [Hugo](https://gohugo.io/) static site generator.

Please [install Hugo](https://gohugo.io/installation/).
- MacOS: `brew install hugo`
- Linux: `sudo snap install hugo` (see the link for particular/alternate distros)
- Windows: see the link

From there, one may `cd` into the main directory and run `hugo server`. This starts up a local deployment of the website that reflects live changes to the content. It's hosted on a `localhost:XXXX` address.

Once you're satisfied with the state of the website, run `hugo build` to generate concrete HTML, commit it to the repository, and it will be momentarily reflected on the website upon completion of the Hugo Github Action.
