function [config_mask] = getAction_Rev(config, invalid_cyl, M)
    c = containers.Map;

    for idx = 1:M
        c(int2str(idx)) = [2*idx-1, 2*idx];
    end

    cyl_index_1 = c(int2str(invalid_cyl(1)))
    r1 = config(cyl_index_1)

    cyl_index_2 = c(int2str(invalid_cyl(2)))
    r2 = config(cyl_index_2)

    d_12 = [r1(1)-r2(1), r1(2)-r2(2)]
    d_12_mag = norm(d_12)

    overlap = 2.1 - d_12_mag;
    half_overlap = overlap/2;

    d_12_hat = d_12/d_12_mag

    action_rev_p = half_overlap * d_12_hat
    action_rev_n = -action_rev_p

    r1_rev = r1 + action_rev_p
    r2_rev = r2 + action_rev_n
    
    config_mask = zeros(1, 2*M)
    config_mask(cyl_index_1) = r1_rev
    config_mask(cyl_index_2) = r2_rev