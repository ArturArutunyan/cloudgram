class Cloudgram < Formula
  desc "Telegram messaging tool"
  homepage "https://github.com/ArturArutunyan/cloudgram"
  url "https://github.com/ArturArutunyan/cloudgram/archive/refs/tags/1.0.0.tar.gz"
  sha256 "c239904c80ebea8d4e1a6725412fc258a1de34618111a41a45617e9226117dcc"

  depends_on "python@3.12"

  def install
    venv_dir = libexec/"venv"
    system "python3", "-m", "venv", venv_dir

    system "#{venv_dir}/bin/pip", "install", "-r", "requirements.txt"

    bin.install "install"

    chmod 0755, bin/"install"
  end

  test do
    system "#{bin}/install", "--help"
  end
end

