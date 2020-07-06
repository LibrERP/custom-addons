#! /bin/bash
# -*- coding: utf-8 -*-
#
# pyxbgen
# Agenzia delle Entrate pyxb generator
#
# This free software is released under GNU Affero GPL3
# author: Antonio M. Vigliotti - antoniomaria.vigliotti@gmail.com
# (C) 2017-2018 by SHS-AV s.r.l. - http://www.shs-av.com - info@shs-av.com
#
THIS=$(basename "$0")
TDIR=$(readlink -f $(dirname $0))
PYTHONPATH=$(echo -e "import sys\nprint str(sys.path).replace(' ','').replace('\"','').replace(\"'\",\"\").replace(',',':')[1:-1]"|python)
for d in $TDIR $TDIR/.. ${PYTHONPATH//:/ } /etc; do
  if [ -e $d/z0librc ]; then
    . $d/z0librc
    Z0LIBDIR=$d
    Z0LIBDIR=$(readlink -e $Z0LIBDIR)
    break
  elif [ -d $d/z0lib ]; then
    . $d/z0lib/z0librc
    Z0LIBDIR=$d/z0lib
    Z0LIBDIR=$(readlink -e $Z0LIBDIR)
    break
  fi
done
if [ -z "$Z0LIBDIR" ]; then
  echo "Library file z0librc not found!"
  exit 2
fi

__version__=0.1.5.7

excl="DatiFatturaMessaggi,FatturaPA_versione_1.1,FatturaPA_versione_1.2,MessaggiTypes"


OPTOPTS=(h        b          k        l        n           O       p          q            u       V           v           x)
OPTDEST=(opt_help opt_branch opt_keep opt_list opt_dry_run opt_OCA opt_nopep8 opt_verbose  opt_uri opt_version opt_verbose opt_exclude)
OPTACTI=(1        "="        1        "1>"     1           1       1          0            "1>"    "*"         1           "=>")
OPTDEFL=(1        ""         0        0        0           0       0          -1            0       ""         -1          "$excl")
OPTMETA=("help"   "ver"      ""       ""       ""          ""      ""         "silent"     ""      "version"   "verbose"   "file")
OPTHELP=("this help"\
 "keep temporary files"\
 "odoo branch; may be 6.1 7.0 8.0 9.0 10.0 11.0 or 12.0"\
 "list xml schemas and module names"\
 "do nothing (dry-run)"\
 "OCA compatible (convert numeric type to string)"\
 "do not apply pep8"\
 "silent mode"\
 "execute uri Agenzia delle Entrate"\
 "show version"\
 "verbose mode"\
 "commma separated module exclusion list; i.e. fornituraIvp,FatturaPA,DatiFattura,DatiFatturaMessaggi")
OPTARGS=()

DISTO=$(xuname "-d")
if [ "$DISTO" == "CentOS" ]; then
  parseoptargs "$@"
else
  echo "Warning! This tool run just under CentOS, version 6 o 7"
  opt_version=0
  opt_help=1
fi
if [ "$opt_version" ]; then
  echo "$__version__"
  exit 0
fi
if [ $opt_help -gt 0 ]; then
  print_help "Agenzia delle Entrate pyxb generator\nPer generare file .py usare switch -u"\
  "(C) 2017-2018 by zeroincombenze(R)\nhttp://wiki.zeroincombenze.org/en/Linux/dev\nAuthor: antoniomaria.vigliotti@gmail.com"
  exit 0
fi
XSD_FILES=("fornituraIvp_2017_v1.xsd" "FatturaPA_versione_1.2.xsd" "FatturaPA_versione_1.1.xsd" "DatiFatturav2.1.xsd" "DatiFatturaMessaggiv2.0.xsd" "MessaggiTypes_v1.1.xsd" "Fattura_VFPR12.xsd" "Fattura_VFSM10.xsd")
MOD_NAMES=("vat_settlement_v_1_0"     "fatturapa_v_1_2"            "fatturapa_v_1_1"            "dati_fattura_v_2_1"  "messaggi_fattura_v_2_0"      "MessaggiTypes_v_1_1"    "fatturapa_v_1_2"    "fatturapa_v_1_0")
bin_path=${PATH//:/ }
for x in $TDIR $TDIR/.. $bin_path; do
  if [ -e $x/pyxbgen ]; then
    PYXBGEN=$x/pyxbgen
    break
  fi
done
TOPEP8=$(which topep8 2>/dev/null)
if [ -z "$TOPEP8" ]; then
  TOPEP8=$(which autopep8 2>/dev/null)
  [ -n "$TOPEP8" ] && TOTEP8="$TOPEP8 -i"
else
  TOTEP8="$TOPEP8 -AeL"
  [ -n "$odoo branch" ] && TOTEP8="$TOPEP8 -b$odoo branch"
fi
if [ -z "$TOPEP8" -a $opt_nopep8 -eq 0 ]; then
  echo "topep8/autopep8 not found!"
  echo "Operations will be executed with switch -p"
fi
cmd=
mdl=
grpl=
OCA_binding=
if [ $opt_OCA -ne 0 ]; then OCA_binding="OCA"; fi
BINDINGS=$TDIR/bindings
SCHEMAS=../data
VALID_COLOR="\e[0;92;40m"
INVALID_COLOR="\e[0;31;40m"
NOP_COLOR="\e[0m"
if [ $opt_list -eq 0 ]; then
   if [ "$PWD" != "$TDIR" ]; then
     [ $opt_verbose -ne 0 ] && echo "\$ cd $TDIR"
     cd $TDIR
   fi
   [ -d $BINDINGS.bak -a  $opt_verbose -ne 0 ] && echo "\$ rm -fR $BINDINGS.bak"
   [ -d $BINDINGS.bak ] && rm -fR $BINDINGS.bak
   [ $opt_verbose -ne 0 ] && echo "\$ mv $BINDINGS $BINDINGS.bak"
   mv $BINDINGS $BINDINGS.bak
fi
[ $opt_verbose -ne 0 ] && echo "\$ mkdir -p $BINDINGS"
mkdir -p $BINDINGS
pushd $BINDINGS ?>/dev/null
[ $opt_verbose -ne 0 ] && echo "\$ cd $PWD"
exclude="(${opt_exclude//,/|})"
for d in $SCHEMAS/*; do
  if [ -d $d ]; then
    x=$(basename $d)
    if [ "$x" != "common" ]; then
      [ $opt_verbose -ne 0 ] && echo "# analyzing directory $d ..."
      if [ -L $d/xmldsig-core-schema.xsd ]; then
        [ $opt_verbose -ne 0 ] && echo "\$ rm -f $d/xmldsig-core-schema.xsd"
        rm -f $d/xmldsig-core-schema.xsd
      fi
      if [ ! -f $d/xmldsig-core-schema.xsd ]; then
        [ $opt_verbose -ne 0 ] && echo "\$ cp $SCHEMAS/common/xmldsig-core-schema.xsd $SCHEMAS/$x/"
        cp $SCHEMAS/common/xmldsig-core-schema.xsd $SCHEMAS/$x/
      fi
    fi
    p=$d
    for x in main liquidazione; do
      if [ -d $d/$x ]; then
        p=$d/$x
        break
      fi
    done
    [ $opt_verbose -ne 0 ] && echo "# searching for schemas into directory $p ..."
    for f in $p/*.xsd; do
      fn=$(basename $f)
      if [[ ! $fn =~ $exclude || $opt_list -ne 0 ]]; then
        # [ $opt_verbose -ne 0 ] && echo ".... parsing file $fn"
        jy=0
        while ((jy<${#XSD_FILES[*]})); do
          xsd="${XSD_FILES[jy]}"
          mdn="${MOD_NAMES[jy]}"
          if [ "$fn" == "$xsd" ]; then
            grp=${mdn:0: -6}
            if [[ $fn =~ $exclude ]]; then
              info="deprecated"
              TEXT_COLOR="$INVALID_COLOR"
            else
              info=""
              TEXT_COLOR="$VALID_COLOR"
            fi
            _xsd=$(printf "%-30.30s" "$xsd")
            _mdn=$(printf "%-20.20s" "$mdn")
            if [ $opt_list -ne 0 ]; then
              echo -e "Found schema $TEXT_COLOR$_xsd$NOP_COLOR module $_mdn (by $grp) $info"
            elif [[ $grpl =~ $grp ]]; then
              echo "Schema $_xsd conflict with prior schema by $grp"
            else
              grpl="$grpl $grp"
              mdl="$mdl $mdn"
              cmd="-u $f -m $mdn $cmd"
            fi
            break
          fi
          ((jy++))
        done
      fi
    done
  fi
done
cmd="$PYXBGEN $cmd --archive-to-file=./ade.wxs"
if [ $opt_list -eq 0 ]; then
  [ $opt_verbose -ne 0 ] && echo "\$ $cmd"
  [ $opt_dry_run -ne 0 ] || eval "$cmd"
  i=./__init__.py
  if [ $opt_dry_run -eq 0 ]; then
    echo " # flake8: noqa" >$i
    echo "# -*- coding: utf-8 -*-" >>$i
    echo "# Copyright 2017-2018 - SHS-AV s.r.l. <http://wiki.zeroincombenze.org/it/Odoo>">>$i
    echo "#                       Associazione Odoo Italia <http://www.odoo-italia.org>">>$i
    echo "# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).">>$i
    echo "#">>$i
    echo "# Generated $(date '+%a %Y-%m-%d %H:%M:%S') by pyxbgen.sh $__version__">>$i
    echo "# by Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>">>$i
    echo "#">>$i
    for m in $mdl; do
      echo "from . import $m">>$i
    done
  fi
  for f in _cm _ds $mdl; do
    fn=$f.py
    [ $opt_verbose -ne 0 ] && echo "\$ $TDIR/pyxbgen.py $fn $SCHEMAS $OCA_binding"
    [ $opt_dry_run -ne 0 -a $opt_keep -ne 0 ] || cp $fn $fn.bak
    [ $opt_dry_run -ne 0 ] || eval $TDIR/pyxbgen.py $fn $SCHEMAS "$OCA_binding"
    if [ $opt_nopep8 -eq 0 ]; then
      [ $opt_verbose -ne 0 ] && echo "\$ $TOPEP8 $fn"
      [ $opt_dry_run -ne 0 ] || $TOPEP8 $fn
    fi
  done
fi
popd ?>/dev/null
if [ $opt_list -eq 0 -a $opt_keep -eq 0 ]; then
  find . -name "*.bak" -delete
  find . -name "*.pyc" -delete
fi
