if [ $_GRABBER_ACTIVATED ]; then
    
    if [ $_PATH_BEFORE_GRABBER_ACTIVATE ]; then
        export PATH=$_PATH_BEFORE_GRABBER_ACTIVATE
    fi

    if [ $_PYTHONPATH_BEFORE_GRABBER_ACTIVATE ]; then
        if [  $_PYTHONPATH_BEFORE_GRABBER_ACTIVATE != 0 ]; then
            export PYTHONPATH=$_PYTHONPATH_BEFORE_GRABBER_ACTIVATE
        else
            unset PYTHONPATH
        fi
    fi

    unset _PATH_BEFORE_GRABBER_ACTIVATE
    unset _PYTHONPATH_BEFORE_GRABBER_ACTIVATE
    unset _GRABBER_ACTIVATED
else
    echo 'Not active'
fi
    