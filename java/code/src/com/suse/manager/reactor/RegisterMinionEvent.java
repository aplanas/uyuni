/**
 * Copyright (c) 2015 SUSE LLC
 *
 * This software is licensed to you under the GNU General Public License,
 * version 2 (GPLv2). There is NO WARRANTY for this software, express or
 * implied, including the implied warranties of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
 * along with this software; if not, see
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
 *
 * Red Hat trademarks are not licensed under GPLv2. No permission is
 * granted to use or replicate Red Hat trademarks that are incorporated
 * in this software or its documentation.
 */
package com.suse.manager.reactor;

import com.redhat.rhn.common.messaging.EventMessage;

/**
 * Event for triggering creation of system records for salt minions.
 */
public class RegisterMinionEvent implements EventMessage {

    private String minionId;

    /**
     * Create a new event to trigger system registration.
     *
     * @param minionIdIn minion to register
     */
    public RegisterMinionEvent(String minionIdIn) {
        if (minionIdIn == null) {
            throw new IllegalArgumentException("minionId cannot be null");
        }
        this.minionId = minionIdIn;
    }

    /**
     * Return constantly 1L here (needed to initialize logging).
     *
     * @return the user that scheduled the event
     */
    public Long getUserId() {
        return 1L;
    }

    /**
     * Return the minion id.
     *
     * @return minion id
     */
    public String getMinionId() {
        return minionId;
    }

    /**
     * {@inheritDoc}
     */
    public String toText() {
        return toString();
    }

    /**
     * {@inheritDoc}
     */
    public String toString() {
        return "RegisterMinionEvent[minionId: " + minionId + "]";
    }
}
