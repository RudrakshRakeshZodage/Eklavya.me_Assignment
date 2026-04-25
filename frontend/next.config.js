/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://13.217.105.1/:path*',
      },
    ]
  },
}

module.exports = nextConfig
