python3 -m PyInstaller \
  --onefile \
  --windowed \
  --name "SevenSegmentApp" \
  --add-data "assets:assets" \
  --hidden-import "PIL" \
  --hidden-import "PIL.Image" \
  --hidden-import "PIL.ImageDraw" \
  --hidden-import "PIL.ImageFont" \
  --hidden-import "PIL.ImageTk" \
  --icon "assets/icon.ico" \
  --clean \
  --noconfirm \
  start.py