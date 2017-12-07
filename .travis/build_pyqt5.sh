PYQT=$TRAVIS_BUILD_DIR/pyqt

SIP_VERSION=4.19.6
PYQT_VERSION=5.8.1
QT_BASE=58
USE_CMAKE=true

sudo add-apt-repository -y ppa:beineri/opt-qt591-trusty
sudo apt-get update
sudo apt-get install -y qt59base
source /opt/qt59/bin/qt59-env.sh

sudo apt-get install -y python3-pyqt5
sudo apt-get install -y qttools5-dev-tools
sudo apt-get install -y pyqt5-dev-tools
# mkdir -p $PYQT
# cd $PYQT

# wget -O sip.tar.gz http://sourceforge.net/projects/pyqt/files/sip/sip-$SIP_VERSION/sip-$SIP_VERSION.tar.gz
# mkdir -p sip
# tar xzf sip.tar.gz -C sip --strip-component=1

# wget -O PyQt.tar.gz  http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-$PYQT_VERSION/PyQt5_gpl-$PYQT_VERSION.tar.gz
# mkdir -p PyQt
# tar xzf PyQt.tar.gz -C PyQt --strip-components=1

# cd $PYQT/sip
# #python configure.py -e $PYQT/include
# python configure.py
# make
# sudo make install

# cd $PYQT/PyQt
# python configure.py --confirm-license --no-designer-plugin -e QtCore -e QtGui -e QtWidgets
# make
# sudo make install