//--------------------------------------------------------------------------
// Copyright (C) 2016-2025 Cisco and/or its affiliates. All rights reserved.
//
// This program is free software; you can redistribute it and/or modify it
// under the terms of the GNU General Public License Version 2 as published
// by the Free Software Foundation.  You may not use, modify or distribute
// this program under any other version of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
//--------------------------------------------------------------------------

// memory_config.h author Joel Cornett <jocornet@cisco.com>

#ifndef MEMORY_CONFIG_H
#define MEMORY_CONFIG_H

#include <cstddef>

struct MemoryConfig
{
    size_t cap = 0;
    unsigned threshold = 0;
    unsigned interval = 1000;
    unsigned prune_target = 1048576;
    bool enabled = false;

    constexpr MemoryConfig() = default;
};

#endif

