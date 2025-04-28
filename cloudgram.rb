class Cloudgram < Formula
  desc "Telegram messaging tool"
  homepage "https://github.com/ArturArutunyan/cloudgram"
  url "https://github.com/ArturArutunyan/cloudgram/archive/refs/tags/1.0.2.tar.gz"
  sha256 "477c38deb7f14f75bfa4afc1e877ffc184e3ac9504e6b73525e6ec69a342d8dd"

  depends_on "python@3.12"

  def install
    venv_dir = libexec/"venv"
    system "python3", "-m", "venv", venv_dir

    system "#{venv_dir}/bin/pip", "install", "-r", "requirements.txt"

    bin.install "cloudgram"

    chmod 0755, bin/"cloudgram"
  end

  test do
    system "#{bin}/cloudgram", "--help"
  end
end

