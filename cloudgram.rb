class Cloudgram < Formula
  desc "Telegram messaging tool"
  homepage "https://github.com/ArturArutunyan/cloudgram"
  url "https://github.com/ArturArutunyan/cloudgram/archive/refs/tags/1.0.3.tar.gz"
  sha256 "7a33feb9cf6a8b6f71d830b80dad9fe915d45e2fd8dc56b857787d8b98eefa25"

  depends_on "python@3.12"

  def install
    venv_dir = libexec/"venv"
    system "python3", "-m", "venv", venv_dir

    system "#{venv_dir}/bin/pip", "install", "-r", "requirements.txt"

    bin.install "cloudgram-install"

    chmod 0755, bin/"cloudgram-install"
  end

  test do
    system "#{bin}/cloudgram", "--help"
  end
end

