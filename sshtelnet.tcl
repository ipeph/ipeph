#!/usr/bin/expect --

proc connectssh {username password hostname} {
	global spawn_id
	set success 1
	spawn ssh $username@$hostname
	expect {
	    "continue connecting (yes/no)?" {
	    	send "yes\r"
	    	exp_continue
	    }
		"Connection refused" {
			connecttelnet $username $password $hostname
		}
	    timeout {
		    connecttelnet $username $password $hostname
	    }
		"Host key verification failed." {
            wait
            puts "here"
            exec ssh-keygen -R $hostname
        }
#        "known_hosts.old" {
#       	wait
#			puts "this"
#			connectssh $username $hostname
#        }
		"?assword:" {
				if { $success == 0 } {
					log_user 1
	    			puts "error user or password incorrect"
	    			exit 1;
				} else {
					incr success -1
					send "$password\r"
			}
			exp_continue
		}
		"#" {
			send "terminal length 0\r"
		}
	}
}

proc conecttelnet {username password hostname} {
    global spawn_id
	spawn telnet $hostname
	set success 1
    expect {
    	"?sername:" {
			if { $success == 0 } {
				log_user 1
    			puts "error user or password incorrect"
    			exit 1;
			} else {
				incr success -1
				send "$username\r"
			}
			exp_continue
		}
		"?assword:" {
			send "$password\r"
			exp_continue
		}
   		timeout {
   			log_user 1
			puts "error could not ssh or telnet devices"
			exit 1;
			exp_continue
		}
    	"?..." {
    		log_user 1
			puts "error could not ssh or telnet devices"
			exit 1;
			exp_continue
		}
		"#" {
			send "terminal length 0\r"
		}
	}
}

set env(TERM) vt100
set timeout 5
set username [lindex $argv 0]
set password [lindex $argv 1]
set hostname [lindex $argv 2]

#login script
log_user 1
connectssh $username $password $hostname

#execute script
expect "#"
send "\r"
expect "#"
log_user 1
send "show version\r"
expect "#"
send "exit\r"

*********************************************

ERROR

*********************************************

[linux]$ ./sshtelnet.tcl febry password 1.1.1.1
spawn ssh mine@1.1.1.1
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
83:24:a5:c4:2c:98:0d:0b:d6:ad:cb:74:12:7e:84:83.
Please contact your system administrator.
Add correct host key in /home/svc_netlog_id/.ssh/known_hosts to get rid of this message.
Offending key in /home/svc_netlog_id/.ssh/known_hosts:152
RSA host key for 1.1.1.1 has changed and you have requested strict checking.
Host key verification failed.
here
/home/svc_netlog_id/.ssh/known_hosts updated.
Original contents retained as /home/svc_netlog_id/.ssh/known_hosts.old
    while executing
"exec ssh-keygen -R $hostname"
    invoked from within
"expect {
	    "continue connecting (yes/no)?" {
	    	send "yes\r"
	    	exp_continue
	    }
		"Connection refused" {
			connecttelnet $username $pass..."
    (procedure "connectssh" line 5)
    invoked from within
"connectssh $username $password $hostname"
    (file "./sshtelnet.tcl" line 91)
