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

