class Cloudgram < Formula
  desc "Telegram messaging tool"
  homepage "https://github.com/ArturArutunyan/cloudgram"
  url "https://github.com/ArturArutunyan/cloudgram/archive/refs/tags/1.0.3.tar.gz"
  sha256 "7a33feb9cf6a8b6f71d830b80dad9fe915d45e2fd8dc56b857787d8b98eefa25"

  depends_on "python@3.12"

  def install
    python = Formula["python@3.12"].opt_bin/"python3.12"
    system python, "-m", "venv", libexec/"venv"

    # Install dependencies first
    system libexec/"venv/bin/pip", "install", "telethon"

    # Copy Python files manually
    libexec.install Dir["*.py"]
    libexec.install "cloudgram" if Dir.exist?("cloudgram")

    (bin/"cloudgram").write <<~EOS
      #!#{libexec}/venv/bin/python
      import sys
      sys.path.insert(0, '#{libexec}')
      from cloudgram import main
      if __name__ == "__main__":
          main()
    EOS
  end

  test do
    system "#{bin}/cloudgram", "--help"
  end
end