if ( ${?_GRABBER_ACTIVATED} ) then
    
    if ( ${?_PATH_BEFORE_GRABBER_ACTIVATE} ) then
        setenv PATH $_PATH_BEFORE_GRABBER_ACTIVATE
    endif

    if ( ${?_PYTHONPATH_BEFORE_GRABBER_ACTIVATE} ) then
        if ( { eval 'test ! -z $_PYTHONPATH_BEFORE_GRABBER_ACTIVATE' } ) then
            setenv PYTHONPATH $_PYTHONPATH_BEFORE_GRABBER_ACTIVATE
        else
            unsetenv PYTHONPATH
        endif
    endif

    unsetenv _PATH_BEFORE_GRABBER_ACTIVATE
    unsetenv _PYTHONPATH_BEFORE_GRABBER_ACTIVATE
    unsetenv _GRABBER_ACTIVATED
else
    echo 'Not active'
endif
    